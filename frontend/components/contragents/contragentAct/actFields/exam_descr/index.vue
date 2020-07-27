<template lang="pug">
  v-col(cols="12")
    v-textarea(
      filled
      v-model="actExamDescr"
      label="Описание"
    )
</template>

<script>
export default {
  computed: {
    actExamDescr: {
      set (actExamDescr) {
        this.$store.commit('act/SET_ACT', { exam_descr: actExamDescr })
      },
      get () {
        return this.$store.state.act.detail.exam_descr
      }
    }
  }
}
</script>
