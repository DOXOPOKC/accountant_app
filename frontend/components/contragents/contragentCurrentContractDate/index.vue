<template lang="pug">
  v-col(cols="3")
    v-menu(
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="currentContractDate"
      transition="scale-transition"
      offset-y
      min-width="290px"
    )
      template(v-slot:activator="{ on }")
        ValidationProvider(rules="required" name="" v-slot="{ errors }")
          v-text-field(
            dense
            readonly
            v-model="currentContractDate"
            label="Дата заключения договора"
            v-on="on"
            :error-messages="errors"
          )
      v-date-picker(v-model="currentContractDate" no-title scrollable)
        v-spacer
        v-btn(text color="primary" @click="menu = false") Отмена
        v-btn(text color="primary" @click="$refs.menu.save(currentContractDate)") OK
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
    currentContractDate: {
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
