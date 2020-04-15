<template lang="pug">
  v-col(cols="3")
    v-text-field(
      v-model="ks"
      label="к/с"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    ks: {
      set (ks) {
        this.$store.commit('contragents/SET_CONTRAGENT', { ks })
      },
      get () {
        return this.$store.state.contragents.detail.ks
      }
    }
  }
}
</script>
