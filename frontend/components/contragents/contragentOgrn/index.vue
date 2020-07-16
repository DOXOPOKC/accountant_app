<template lang="pug">
  v-col(cols="2")
    v-text-field(
      dense
      v-model="ogrn"
      label="ОГРН"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    ogrn: {
      set (ogrn) {
        this.$store.commit('contragents/SET_CONTRAGENT', { ogrn })
      },
      get () {
        return this.$store.state.contragents.detail.ogrn
      }
    }
  }
}
</script>
