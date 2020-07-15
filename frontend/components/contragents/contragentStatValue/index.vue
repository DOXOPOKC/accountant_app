<template lang="pug">
  v-col(cols="5")
    ValidationProvider(rules="required" v-slot="{ errors }")
      v-text-field(
        dense
        v-model="statValue"
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
    statValue: {
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
