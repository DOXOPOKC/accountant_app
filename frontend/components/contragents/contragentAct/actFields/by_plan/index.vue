<template lang="pug">
  v-col(cols="12")
    v-checkbox(
      v-model="actPlan"
      label="- самостоятельно в результате планового обхода"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    actPlan: {
      set (actPlan) {
        this.$store.commit('act/SET_ACT', { by_plan: actPlan })
      },
      get () {
        return this.$store.state.act.detail.by_plan
      }
    }
  }
}
</script>
