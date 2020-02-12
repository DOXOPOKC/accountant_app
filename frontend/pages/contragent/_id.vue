<template lang="pug">
  v-row(
    class="fill-height"
    justify="center"
    align="start"
    no-gutters
  )
    v-col(
      xs12
      sm8
      md6
    )
      v-card(
        flat
        exact
      )
        v-card-title(class="headline font-weight-light px-10")
          | Контрагент № {{ contragent.id }}
          v-spacer
          v-btn(
            outlined
            class="text-capitalize"
            color="primary"
            :to="'/contragent/' + $route.params.id + '/packages/'"
          ) Посмотреть пакеты
        v-card-text
          contragent-bank
          contragent-bik
          contragent-class
          contragent-contract-accept-date
          contragent-creation-date
          contragent-current-contract-date
          contragent-current-date
          contragent-current-user
          contragent-dadata-name
          contragent-debt
          contragent-director-name
          contragent-director-status
          contragent-excell-name
          contragent-id
          contragent-inn
          contragent-is-func
          contragent-kpp
          contragent-ks
          contragent-legal-address
          contragent-norm-value
          contragent-number-contract
          contragent-ogrn
          contragent-okved
          contragent-opf
          contragent-physical-address
          contragent-platform
          contragent-rs
          contragent-signed-user
          contragent-stat-value
        v-card-actions(class="px-10 py-6")
          | {{contragent}}
          //- v-btn(
          //-   color="primary"
          //-   @click=""
          //-   to="put /contragents/{id}/packages/{package_id}"
          //- )
          //-   | Перегенерировать
          v-btn(
            @click="GENERATE_PACKAGE"
          )
            | Сгенерировать пакет
          v-spacer
          v-btn(
            color="primary"
            @click="UPDATE_CONTRAGENT"
          )
            | Сохранить
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { ValidationProvider, ValidationObserver } from 'vee-validate'

import contragentBank from '@/components/contragents/contragentBank'
import contragentBik from '@/components/contragents/contragentBik'
import contragentClass from '@/components/contragents/contragentClass'
import contragentContractAcceptDate from '@/components/contragents/contragentContractAcceptDate'
import contragentCreationDate from '@/components/contragents/contragentCreationDate'
import contragentCurrentContractDate from '@/components/contragents/contragentCurrentContractDate'
import contragentCurrentDate from '@/components/contragents/contragentCurrentDate'
import contragentCurrentUser from '@/components/contragents/contragentCurrentUser'
import contragentDadataName from '@/components/contragents/contragentDadataName'
import contragentDebt from '@/components/contragents/contragentDebt'
import contragentDirectorName from '@/components/contragents/contragentDirectorName'
import contragentDirectorStatus from '@/components/contragents/contragentDirectorStatus'
import contragentExcellName from '@/components/contragents/contragentExcellName'
import contragentId from '@/components/contragents/contragentId'
import contragentInn from '@/components/contragents/contragentInn'
import contragentIsFunc from '@/components/contragents/contragentIsFunc'
import contragentKpp from '@/components/contragents/contragentKpp'
import contragentKs from '@/components/contragents/contragentKs'
import contragentLegalAddress from '@/components/contragents/contragentLegalAddress'
import contragentNormValue from '@/components/contragents/contragentNormValue'
import contragentNumberContract from '@/components/contragents/contragentNumberContract'
import contragentOgrn from '@/components/contragents/contragentOgrn'
import contragentOkved from '@/components/contragents/contragentOkved'
import contragentOpf from '@/components/contragents/contragentOpf'
import contragentPhysicalAddress from '@/components/contragents/contragentPhysicalAddress'
import contragentPlatform from '@/components/contragents/contragentPlatform'
import contragentRs from '@/components/contragents/contragentRs'
import contragentSignedUser from '@/components/contragents/contragentSignedUser'
import contragentStatValue from '@/components/contragents/contragentStatValue'

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    contragentBank,
    contragentBik,
    contragentClass,
    contragentContractAcceptDate,
    contragentCreationDate,
    contragentCurrentContractDate,
    contragentCurrentDate,
    contragentCurrentUser,
    contragentDadataName,
    contragentDebt,
    contragentDirectorName,
    contragentDirectorStatus,
    contragentExcellName,
    contragentId,
    contragentInn,
    contragentIsFunc,
    contragentKpp,
    contragentKs,
    contragentLegalAddress,
    contragentNormValue,
    contragentNumberContract,
    contragentOgrn,
    contragentOkved,
    contragentOpf,
    contragentPhysicalAddress,
    contragentPlatform,
    contragentRs,
    contragentSignedUser,
    contragentStatValue
  },
  async asyncData ({ $axios, store, params }) {
    await store.dispatch('contragents/FETCH_CONTRAGENT', params.id)
  },
  data: () => ({}),
  computed: {
    ...mapState({
      contragentInfo: (state) => {
        const data = state.contragents.detail
        const result = Object.keys(data).map((key) => {
          const test = {}
          test[key] = `${data[key]}`
          return test
        })
        return result
      },
      contragent: state => state.contragents.detail
    }),
    panels () {
      return [...Array(this.contragentInfo.length).keys()]
    }
  },
  methods: {
    ...mapActions({
      UPDATE_CONTRAGENT: 'contragents/UPDATE_CONTRAGENT',
      GENERATE_PACKAGE: 'packages/GENERATE_PACKAGE'
    })
  }
}
</script>
