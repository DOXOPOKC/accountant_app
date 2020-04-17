<template lang="pug">
  v-col(cols="6")
    v-text-field(
      v-model="bik"
      label="БИК"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    bik: {
      set (bik) {
        this.$store.commit('contragents/SET_CONTRAGENT', { bik })
      },
      get () {
        return this.$store.state.contragents.detail.bik
      }
    }
  }
}
</script>
