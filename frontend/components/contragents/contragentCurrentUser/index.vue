<template lang="pug">
  v-col(cols="12")
    v-text-field(
      disabled
      dense
      v-model="current_user"
      label="Текущий пользователь"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    current_user: {
      set (currentUser) {
        this.$store.commit('contragents/SET_CONTRAGENT', { current_user: currentUser })
      },
      get () {
        return this.$store.state.contragents.detail.current_user
      }
    }
  }
}
// disabled
</script>
