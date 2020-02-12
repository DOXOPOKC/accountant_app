<template lang="pug">
  v-col(cols="12")
    v-text-field(
      v-model="rs"
      label="р/с"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    rs: {
      set (rs) {
        this.$store.commit('contragents/SET_CONTRAGENT', { rs })
      },
      get () {
        return this.$store.state.contragents.detail.rs
      }
    }
  }
}
</script>
