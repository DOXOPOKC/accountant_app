<template lang="pug">
  v-col(cols="12")
    v-textarea(
      filled
      v-model="actExamResult"
      label="В результате проведенного осмотра установлено"
    )
</template>

<script>
export default {
  computed: {
    actExamResult: {
      set (actExamResult) {
        this.$store.commit('act/SET_ACT', { exam_result: actExamResult })
      },
      get () {
        return this.$store.state.act.detail.exam_result
      }
    }
  }
}
</script>
