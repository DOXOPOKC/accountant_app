<template lang="pug">
  v-col(cols="12")
    v-menu(
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="contract_accept_date"
      transition="scale-transition"
      offset-y
      min-width="290px"
    )
      template(v-slot:activator="{ on }")
        v-text-field(
          v-model="contract_accept_date"
          label="Дата начала оказания услуг"
          readonly
          v-on="on"
        )
      v-date-picker(v-model="contract_accept_date" no-title scrollable)
        v-spacer
        v-btn(text color="primary" @click="menu = false") Cancel
        v-btn(text color="primary" @click="$refs.menu.save(contract_accept_date)") OK
</template>

<script>
export default {
  data: () => ({
    menu: false
  }),
  computed: {
    contract_accept_date: {
      set (contractAcceptDate) {
        this.$store.commit('contragents/SET_CONTRAGENT', { contract_accept_date: contractAcceptDate })
      },
      get () {
        return this.$store.state.contragents.detail.contract_accept_date
      }
    }
  }
}
// date picker
</script>
