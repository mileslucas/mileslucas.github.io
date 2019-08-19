<template>
  <object id="pdf" data="/CV.pdf" type="application/pdf">
    <embed src="/CV.pdf" />
  </object>
</template>

<style scoped>
#pdf {
  width: 90%;
  height: 40rem;
  margin-right: auto;
  margin-left: auto;
  display: block;
}
@media screen and (max-width: 28rem) {
  #pdf {
    display: none;
  }
}
</style>