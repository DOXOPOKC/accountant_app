<template lang="pug">
  v-col(cols="3")
    v-text-field(
      dense
      v-model="platform"
      label="Номер площадки"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    platform: {
      set (platform) {
        this.$store.commit('contragents/SET_CONTRAGENT', { platform })
      },
      get () {
        return this.$store.state.contragents.detail.platform
      }
    }
  }
}
</script>
