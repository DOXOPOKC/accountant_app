<template lang="pug">
  v-col(cols="12")
    v-text-field(
      v-model="actAddress"
      label="Адрес строения"
    )
</template>

<script>
export default {
  computed: {
    actAddress: {
      set (actAddress) {
        this.$store.commit('act/SET_ACT', { address: actAddress })
      },
      get () {
        return this.$store.state.act.detail.address
      }
    }
  }
}
</script>
