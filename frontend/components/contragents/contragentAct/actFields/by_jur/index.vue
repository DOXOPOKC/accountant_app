<template lang="pug">
  v-col(cols="12")
    v-checkbox(
      v-model="actJur"
      label="- обращение юридических лиц "
    )
    v-text-field(
      v-if="actJur"
      v-model="actJurData"
    )
</template>

<script>
export default {
  name: '',
  data: () => ({}),
  computed: {
    actJur: {
      set (actJur) {
        this.$store.commit('act/SET_ACT', { by_jur: actJur })
      },
      get () {
        return this.$store.state.act.detail.by_jur
      }
    },
    actJurData: {
      set (actJurData) {
        this.$store.commit('act/SET_ACT', { jur_data: actJurData })
      },
      get () {
        return this.$store.state.act.detail.jur_data
      }
    }
  }
}
</script>
