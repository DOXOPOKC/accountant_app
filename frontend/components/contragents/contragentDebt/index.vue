<template lang="pug">
  v-col(cols="3")
    v-text-field(
      dense
      readonly
      v-model="debt"
      label="Задолжность"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    debt: {
      set (debt) {
        this.$store.commit('contragents/SET_CONTRAGENT', { debt })
      },
      get () {
        return this.$store.state.contragents.detail.debt
      }
    }
  }
}
// disabled
</script>
