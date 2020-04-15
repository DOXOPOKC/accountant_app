<template lang="pug">
  v-col(cols="6")
    v-menu(
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="current_contract_date"
      transition="scale-transition"
      offset-y
      min-width="290px"
    )
      template(v-slot:activator="{ on }")
        ValidationProvider(rules="required" name="" v-slot="{ errors }")
          v-text-field(
            v-model="current_contract_date"
            label="Дата заключения договора"
            readonly
            v-on="on"
            :error-messages="errors"
          )
      v-date-picker(v-model="current_contract_date" no-title scrollable)
        v-spacer
        v-btn(text color="primary" @click="menu = false") Cancel
        v-btn(text color="primary" @click="$refs.menu.save(current_contract_date)") OK
</template>

<script>
import { ValidationProvider } from 'vee-validate'

export default {
  components: {
    ValidationProvider
  },
  data: () => ({
    menu: false
  }),
  computed: {
    current_contract_date: {
      set (currentContractDate) {
        this.$store.commit('contragents/SET_CONTRAGENT', { current_contract_date: currentContractDate })
      },
      get () {
        return this.$store.state.contragents.detail.current_contract_date
      }
    }
  }
}
// date picker
</script>
