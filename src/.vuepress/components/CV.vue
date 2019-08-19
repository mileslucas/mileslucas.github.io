<template>
  <object id="pdf" data="/CV.pdf" type="application/pdf">
    <embed src="/CV.pdf" />
  </object>
</template>

<style lang="stylus">
#pdf {
  width: 90%;
  height: 40rem;
  margin-right: auto;
  margin-left: auto;
  display: block;
}
@media (max-width: $MQMobile) {
  #pdf {
    display: none;
  }
}
</style>