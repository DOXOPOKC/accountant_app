<template lang="pug">
  v-col(cols="12")
    v-text-field(
      v-model="actNumber"
      label="Номер акта"
    )
</template>

<script>
export default {
  name: '',
  data: () => ({}),
  computed: {
    actNumber: {
      set (actNumber) {
        this.$store.commit('act/SET_ACT', { act_number: actNumber })
      },
      get () {
        return this.$store.state.act.detail.act_number
      }
    }
  }
}
</script>
