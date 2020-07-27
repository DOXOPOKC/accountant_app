<template lang="pug">
  v-col(cols="12")
    v-textarea(
      filled
      v-model="actEvidence"
      label="Наименование фото и видео материалов"
    )
</template>

<script>
export default {
  computed: {
    actEvidence: {
      set (actEvidence) {
        this.$store.commit('act/SET_ACT', { evidence: actEvidence })
      },
      get () {
        return this.$store.state.act.detail.evidence
      }
    }
  }
}
</script>
