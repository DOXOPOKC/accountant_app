<template lang="pug">
  v-col(cols="12")
    v-text-field(
      disabled
      v-model="signed_user"
      label="Уполномоченное лицо"
    )
</template>

<script>
export default {
  data: () => ({
    status: [true, false]
  }),
  computed: {
    signed_user: {
      set (signedUser) {
        this.$store.commit('contragents/SET_CONTRAGENT', { signed_user: signedUser })
      },
      get () {
        return this.$store.state.contragents.detail.signed_user
      }
    }
  }
}
// disabled
</script>
