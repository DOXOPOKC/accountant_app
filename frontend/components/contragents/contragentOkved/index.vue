<template lang="pug">
  v-col(cols="1")
    v-text-field(
      dense
      v-model="okved"
      label="ОКВЕД"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    okved: {
      set (okved) {
        this.$store.commit('contragents/SET_CONTRAGENT', { okved })
      },
      get () {
        return this.$store.state.contragents.detail.okved
      }
    }
  }
}
// disabled
</script>
