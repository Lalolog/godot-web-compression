const originalFetch = window.fetch;
const supportsCompressionAPI = "DecompressionStream" in window;

const files = ["index.wasm", "index.pck"];

async function decompressIfNeeded(response) {
  try {
    if (response.headers.get("Content-Encoding") === "gzip") {
      return response;
    }

    const responseClone = response.clone();
    const buffer = await responseClone.arrayBuffer();
    const uint8 = new Uint8Array(buffer);

    if (uint8[0] === 0x1f && uint8[1] === 0x8b) {
      if (supportsCompressionAPI) {
        const stream = response.body.pipeThrough(
          new DecompressionStream("gzip"),
        );
        return new Response(stream);
      }
      return new Response(fflate.decompressSync(uint8));
    }
    return new Response(buffer);
  } catch (error) {
    console.error(`Decompression error for ${response.url}:`, error);
    return response;
  }
}

window.fetch = async function (resource, options) {
  if (!files.includes(resource)) return originalFetch(resource, options);

  try {
    const response = await originalFetch(resource + ".gz");
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
    return await decompressIfNeeded(response);
  } catch (error) {
    console.error(`Error processing ${resource}:`, error);
    try {
      console.log(`Attempting to load uncompressed: ${resource}`);
      const fallbackResponse = await originalFetch(resource);
      if (!fallbackResponse.ok)
        throw new Error(`HTTP error: ${fallbackResponse.status}`);
      return fallbackResponse;
    } catch (fallbackError) {
      console.error(`Fallback for ${resource} failed:`, fallbackError);
      throw fallbackError;
    }
  }
};
