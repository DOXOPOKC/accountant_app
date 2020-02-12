<template lang="pug">
  v-col(cols="12")
    v-text-field(
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
