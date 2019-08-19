<template>
  <div v-if="render">
    <object
      id="pdf"
      data="/CV.pdf"
      type="application/pdf"
      width="80%"
      height="600rem"
      style="
        
        "
    >
      <embed src="/CV.pdf" />
    </object>
  </div>
  <div v-else>
    <a href="/CV.pdf">Download link</a>
  </div>
</template>

<script>
const pdfSupport = require("browser-pdf-support");

export default {
  data() {
    return {
      render: pdfSupport()
    };
  }
};
</script>

<style scoped>
#pdf {
  margin-right: auto;
  margin-left: auto;
  display: block;
}
</style>