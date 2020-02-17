<template lang="pug">
  v-col(cols="12")
    ValidationProvider(rules="required" v-slot="{ errors }")
      v-select(
        item-text="name"
        item-value="id"
        v-model="norm_value"
        :items="normList"
        label="Норматив"
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
      normList: state => state.contragents.normList
    }),
    norm_value: {
      set (normValue) {
        this.$store.commit('contragents/SET_CONTRAGENT', { norm_value: normValue })
      },
      get () {
        return this.$store.state.contragents.detail.norm_value
      }
    }
  },
  async mounted () {
    await this.$store.dispatch('contragents/FETCH_NORM_LIST')
  }
}
// dropdown
// endpoint : http://localhost/api/norms/ { id: 1, name: "string" }
</script>
