<template lang="pug">
  v-col(cols="3")
    v-menu(
      ref="contractAcceptDateMenu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="contractAcceptDate"
      transition="scale-transition"
      offset-y
      min-width="290px"
    )
      template(v-slot:activator="{ on }")
        v-text-field(
          dense
          readonly
          v-model="contractAcceptDate"
          label="Дата начала оказания услуг"
          v-on="on"
        )
      v-date-picker(v-model="contractAcceptDate" no-title scrollable)
        v-spacer
        v-btn(text color="primary" @click="menu = false") Отмена
        v-btn(text color="primary" @click="$refs.contractAcceptDateMenu.save(contractAcceptDate)") OK
</template>

<script>
export default {
  data: () => ({
    menu: false
  }),
  computed: {
    contractAcceptDate: {
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
