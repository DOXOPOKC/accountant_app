<template lang="pug">
  v-col(cols="2")
    v-text-field(
      dense
      v-model="opf"
      label="Номер паспорта"
    )
</template>

<script>
import PassportDate from '@/components/contragentPassport/PassportDate'
import PassportNumber from '@/components/contragentPassport/PassportNumber'
import PassportOrigin from '@/components/contragentPassport/PassportOrigin'

export default {
  components: [
    PassportDate,
    PassportNumber,
    PassportOrigin
  ],
  data: () => ({}),
  computed: {
    opf: {
      set (opf) {
        this.$store.commit('contragents/SET_CONTRAGENT', { opf })
      },
      get () {
        return this.$store.state.contragents.detail.opf
      }
    }
  }
}
</script>
