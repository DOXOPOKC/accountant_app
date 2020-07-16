<template lang="pug">
  v-col(cols="12")
    v-row(no-gutters)
        passport-date
        passport-number
        passport-origin
</template>

<script>
import PassportDate from '@/components/contragents/contragentPassport/PassportDate'
import PassportNumber from '@/components/contragents/contragentPassport/PassportNumber'
import PassportOrigin from '@/components/contragents/contragentPassport/PassportOrigin'

export default {
  components: {
    PassportDate,
    PassportNumber,
    PassportOrigin
  }
}
</script>
