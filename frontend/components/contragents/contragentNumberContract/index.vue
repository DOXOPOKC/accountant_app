<template lang="pug">
  v-col(cols="12" align="center")
    v-text-field(
      v-if="!!numberContract"
      dense
      readonly
      v-model="numberContract"
      label="Номер контракта"
    )
    v-dialog(
      v-else
      v-model="numberContractDialogState"
      max-width="600px"
    )
      template(
        v-slot:activator="{ on }"
      )
        v-btn(
          text small outlined rounded block
          color="primary"
          class="my-4"
          v-on="on"
        ) Добавить номер контракта
      v-card(
        outlined
      )
        v-card-title Введите номер контракта
        v-card-text
          v-text-field(
            dense
            v-model="numberContract"
          )
        v-card-actions
          v-spacer
          v-btn(color="blue darken-1" text @click="closeNumberContractDialogState") Закрыть
          v-btn(color="blue darken-1" text @click="test") Отправить
</template>

<script>
import { mapActions } from 'vuex'
import { types } from '~/store/contragents'

export default {
  data: () => ({
    numberContractDialogState: false
  }),
  computed: {
    numberContract: {
      set (numberContractValue) {
        this.$store.commit('contragents/SET_CONTRAGENT', { number_contract: Object.assign({}, this.$store.state.contragents.detail.number_contract, { number: numberContractValue }) })
      },
      get () {
        return this.$store.state.contragents.detail.number_contract.number
      }
    }
  },
  methods: {
    ...mapActions('contragents', [types.UPDATE_CONTRACT]),
    closeNumberContractDialogState () {
      this.numberContractDialogState = false
      this.numberContract = ''
    },
    async test () {
      await this.UPDATE_CONTRACT()
      this.numberContractDialogState = false
    }
  }
}
</script>
