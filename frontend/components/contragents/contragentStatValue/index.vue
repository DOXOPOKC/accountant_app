<template lang="pug">
  v-col(cols="12")
    v-text-field(
      v-model="stat_value"
      label="Количественный показатель"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    stat_value: {
      set (statValue) {
        this.$store.commit('contragents/SET_CONTRAGENT', { stat_value: statValue })
      },
      get () {
        return this.$store.state.contragents.detail.stat_value
      }
    }
  }
}
</script>
