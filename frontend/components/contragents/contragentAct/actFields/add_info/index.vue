<template lang="pug">
  v-col(cols="12")
    v-textarea(
      filled
      v-model="actAddInfo"
      label="Дополнительная информация"
    )
</template>

<script>
export default {
  computed: {
    actAddInfo: {
      set (actAddInfo) {
        this.$store.commit('act/SET_ACT', { add_info: actAddInfo })
      },
      get () {
        return this.$store.state.act.detail.add_info
      }
    }
  }
}
</script>
