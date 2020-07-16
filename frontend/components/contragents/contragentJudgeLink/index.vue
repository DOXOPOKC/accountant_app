<template lang="pug">
  v-col(cols="12")
    v-text-field(
      dense
      v-model="judgeLink"
      label="Ссылка на сайт суда"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    judgeLink: {
      set (judgeLink) {
        this.$store.commit('contragents/SET_CONTRAGENT', { judge_link: judgeLink })
      },
      get () {
        return this.$store.state.contragents.detail.judge_link
      }
    }
  }
}
</script>
