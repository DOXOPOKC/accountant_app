<template lang="pug">
  v-row(
    no-gutters
    class="fill-height"
    align="center"
    justify="center"
  )
    v-col(
      cols="6"
      class="fill-height"
    )
      v-card(
        outlined
        flat
        exact
        class="fill-height"
        tile
      )
        ValidationObserver(ref="observer" v-slot="{ handleSubmit }" tag="div")
          v-card-title(class="headline font-weight-light")
            | Контрагент № {{ contragent.id }}
            v-spacer
            contragent-is-func
          v-card-subtitle {{ contragentClass }}
          v-card-text(class="pa-0")
            v-form
              v-row(no-gutters)
                v-expansion-panels(
                  v-model="panel"
                  accordion
                  multiple
                  focusable
                  flat
                  tile
                )
                  v-expansion-panel
                    v-expansion-panel-header Информация о контрагенте
                    v-expansion-panel-content(class="mt-8")
                      v-row(no-gutters)
                        contragent-excell-name
                        contragent-physical-address
                        contragent-passport
                  v-expansion-panel
                    v-expansion-panel-header Юридическая информация
                    v-expansion-panel-content(class="mt-8")
                      v-row(no-gutters)
                        contragent-director-status
                        contragent-director-name
                        contragent-dadata-name
                        contragent-legal-address
                        contragent-inn
                        contragent-kpp
                        contragent-ogrn
                        contragent-okved
                        contragent-opf
                        contragent-creation-date
                  v-expansion-panel
                    v-expansion-panel-header Платежная информация
                    v-expansion-panel-content(class="mt-8")
                      v-row(no-gutters)
                        contragent-bank
                        contragent-rs
                        contragent-ks
                        contragent-bik
                  v-expansion-panel
                    v-expansion-panel-header Данные об отходообразовании
                    v-expansion-panel-content(class="mt-8")
                      v-row(no-gutters)
                        contragent-contract-accept-date
                        contragent-current-date
                        contragent-current-contract-date
                        contragent-debt
                        contragent-number-contract
                        contragent-norm-value
                        contragent-stat-value
                        contragent-platform
                        contragent-signed-user
                  v-expansion-panel
                    v-expansion-panel-header Юридическое лицо
                    v-expansion-panel-content(class="mt-8")
                      v-row(no-gutters)
                        contragent-debt-periond
                        contragent-fss-link
                        contragent-judge-link
                        contragent-personal-number
                        contragent-snils
          v-card-actions(class="px-6 pt-2")
            v-spacer
            v-btn(
              text
              tile
              outlined
              @click="handleSubmit(GENERATE_PACKAGE)"
            )
              | Сгенерировать пакет
            v-btn(
              color="primary"
              text
              tile
              outlined
              @click="handleSubmit(UPDATE_CONTRAGENT)"
            )
              | Сохранить
    v-col(
      cols="6"
      class="fill-height"
    )
      nuxt-child
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

import contragentDebtPeriond from '@/components/contragents/contragentDebtPeriond'
import contragentFssLink from '@/components/contragents/contragentFssLink'
import contragentJudgeLink from '@/components/contragents/contragentJudgeLink'
import contragentPassport from '@/components/contragents/contragentPassport'
import contragentPersonalNumber from '@/components/contragents/contragentPersonalNumber'
import contragentSnils from '@/components/contragents/contragentSnils'

import packagesList from '@/components/packages'

export default {
  components: {
    packagesList,
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
    contragentStatValue,
    contragentDebtPeriond,
    contragentFssLink,
    contragentJudgeLink,
    contragentPersonalNumber,
    contragentSnils,
    contragentPassport
  },
  async asyncData ({ $axios, store, params }) {
    await store.dispatch('contragents/FETCH_CONTRAGENT', params.contragentId)
  },
  data: () => ({
    testComp: [
      'contragent-class',
      'contragent-excell-name',
      'contragent-dadata-name',
      'contragent-director-status',
      'contragent-director-name',
      'contragent-legal-address',
      'contragent-physical-address',
      'contragent-inn',
      'contragent-kpp',
      'contragent-ogrn',
      'contragent-okved',
      'contragent-opf',
      'contragent-rs',
      'contragent-ks',
      'contragent-bank',
      'contragent-bik',
      'contragent-creation-date',
      'contragent-contract-accept-date',
      'contragent-current-date',
      'contragent-current-contract-date',
      'contragent-debt',
      'contragent-number-contract',
      'contragent-norm-value',
      'contragent-stat-value',
      'contragent-platform',
      'contragent-signed-user'
    ],
    classTypes: [
      { value: 0, text: '' },
      { value: 1, text: 'Юридическое лицо без договора' },
      { value: 2, text: 'Юридическое лицо с договором' },
      { value: 3, text: 'ИЖС без договора' },
      { value: 4, text: 'ИЖС с договором' },
      { value: 5, text: 'Физическое лицо' }
    ],
    panel: [0, 3]
  }),
  computed: {
    ...mapState({
      contragent: state => state.contragents.detail
    }),
    contragentClass: {
      set (contragentClass) {
        this.$store.commit('contragents/SET_CONTRAGENT', { klass: contragentClass })
      },
      get () {
        const contragentClassType = this.$store.state.contragents.detail.klass
        const contragentClassTypeText = this.classTypes.find(item => item.value === contragentClassType).text
        return contragentClassTypeText
      }
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
