<template lang="pug">
  v-col(cols="12")
    ValidationProvider(rules="required" v-slot="{ errors }")
      v-select(
          item-text="name"
          item-value="id"
          v-model="signed_user"
          :items="signUsers"
          label="Уполномоченное лицо"
          :error-messages="errors"
        )
</template>

<script>
import { mapState } from 'vuex'
import { ValidationProvider } from 'vee-validate'

export default {
  components: {
    ValidationProvider
  },
  data: () => ({}),
  computed: {
    ...mapState({
      signUsers: state => state.contragents.signUsers
    }),
    signed_user: {
      set (signedUser) {
        this.$store.commit('contragents/SET_CONTRAGENT', { signed_user: signedUser })
      },
      get () {
        return this.$store.state.contragents.detail.signed_user
      }
    }
  },
  async mounted () {
    await this.$store.dispatch('contragents/FETCH_SIGN_USERS_LIST')
  }
}
// disabled
</script>
