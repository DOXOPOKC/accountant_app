<template lang="pug">
  v-col(cols="12")
    ValidationProvider(rules="required" v-slot="{ errors }")
      v-text-field(
        v-model="stat_value"
        label="Количественный показатель"
        :error-messages="errors"
      )
</template>

<script>
import { ValidationProvider } from 'vee-validate'

export default {
  components: {
    ValidationProvider
  },
  data: () => ({}),
  computed: {
    stat_value: {
      set (statValue) {
        this.$store.commit('contragents/SET_CONTRAGENT', { stat_value: statValue })
      },
      get () {
        return this.$store.state.contragents.detail.stat_value
      }
    }
  }
}
</script>
