<template lang="pug">
  v-col(cols="3")
    v-text-field(
      dense
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
