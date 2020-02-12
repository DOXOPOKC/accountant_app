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
          v-text-field(
            v-model="klass"
          )
          v-text-field(
            v-model="excell_name"
          )
          v-text-field(
            v-model="dadata_name"

          )
          v-text-field(
            v-model="debt"

          )
          v-text-field(
            v-model="inn"

          )
          v-text-field(
            v-model="ogrn"

          )
          v-text-field(
            v-model="kpp"

          )
          v-text-field(
            v-model="rs"

          )
          v-text-field(
            v-model="ks"

          )
          v-text-field(
            v-model="bank"

          )
          v-text-field(
            v-model="bik"

          )
          v-text-field(
            v-model="opf"

          )
          v-text-field(
            v-model="director_status"

          )
          v-text-field(
            v-model="director_name"

          )
          v-text-field(
            v-model="creation_date"

          )
          v-text-field(
            v-model="is_func"

          )
          v-text-field(
            v-model="okved"

          )
          v-text-field(
            v-model="physical_address"

          )
          v-text-field(
            v-model="legal_address"

          )
          v-text-field(
            v-model="stat_value"

          )
          v-text-field(
            v-model="contract_accept_date"

          )
          v-text-field(
            v-model="current_date"

          )
          v-text-field(
            v-model="current_contract_date"

          )
          v-text-field(
            v-model="platform"

          )
          v-text-field(
            v-model="norm_value"

          )
          v-text-field(
            v-model="number_contract"

          )
          v-text-field(
            v-model="signed_user"

          )
          v-text-field(
            v-model="current_user"
          )
        v-card-actions(class="px-10 py-6")
          //- v-btn(
          //-   color="primary"
          //-   @click=""
          //-   to="put /contragents/{id}/packages/{package_id}"
          //- )
          //-   | Перегенерировать
          | {{ contragent }}
          v-btn(
            color="primary"
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

// import {
//   contragentBank,
//   contragentBik,
//   contragentClass
// } from '~/components/contragents'

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  async asyncData ({ $axios, store, params }) {
    await store.dispatch('contragents/FETCH_CONTRAGENT', params.id)
  },
  data: () => ({
    test: 1488
  }),
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
    },
    klass: {
      set (klass) {
        this.$store.commit('contragents/SET_CONTRAGENT', { klass })
      },
      get () {
        return this.$store.state.contragents.detail.klass
      }
    },
    excell_name: {
      set (excellName) {
        this.$store.commit('contragents/SET_CONTRAGENT', { excell_name: excellName })
      },
      get () {
        return this.$store.state.contragents.detail.excell_name
      }
    },
    dadata_name: {
      set (dadataName) {
        this.$store.commit('contragents/SET_CONTRAGENT', { dadata_name: dadataName })
      },
      get () {
        return this.$store.state.contragents.detail.dadata_name
      }
    },
    debt: {
      set (debt) {
        this.$store.commit('contragents/SET_CONTRAGENT', { debt })
      },
      get () {
        return this.$store.state.contragents.detail.debt
      }
    },
    inn: {
      set (inn) {
        this.$store.commit('contragents/SET_CONTRAGENT', { inn })
      },
      get () {
        return this.$store.state.contragents.detail.inn
      }
    },
    ogrn: {
      set (ogrn) {
        this.$store.commit('contragents/SET_CONTRAGENT', { ogrn })
      },
      get () {
        return this.$store.state.contragents.detail.ogrn
      }
    },
    kpp: {
      set (kpp) {
        this.$store.commit('contragents/SET_CONTRAGENT', { kpp })
      },
      get () {
        return this.$store.state.contragents.detail.kpp
      }
    },
    rs: {
      set (rs) {
        this.$store.commit('contragents/SET_CONTRAGENT', { rs })
      },
      get () {
        return this.$store.state.contragents.detail.rs
      }
    },
    ks: {
      set (ks) {
        this.$store.commit('contragents/SET_CONTRAGENT', { ks })
      },
      get () {
        return this.$store.state.contragents.detail.ks
      }
    },
    bank: {
      set (bank) {
        this.$store.commit('contragents/SET_CONTRAGENT', { bank })
      },
      get () {
        return this.$store.state.contragents.detail.bank
      }
    },
    bik: {
      set (bik) {
        this.$store.commit('contragents/SET_CONTRAGENT', { bik })
      },
      get () {
        return this.$store.state.contragents.detail.bik
      }
    },
    opf: {
      set (opf) {
        this.$store.commit('contragents/SET_CONTRAGENT', { opf })
      },
      get () {
        return this.$store.state.contragents.detail.opf
      }
    },
    director_status: {
      set (directorStatus) {
        this.$store.commit('contragents/SET_CONTRAGENT', { director_status: directorStatus })
      },
      get () {
        return this.$store.state.contragents.detail.director_status
      }
    },
    director_name: {
      set (directorName) {
        this.$store.commit('contragents/SET_CONTRAGENT', { director_name: directorName })
      },
      get () {
        return this.$store.state.contragents.detail.director_name
      }
    },
    creation_date: {
      set (creationDate) {
        this.$store.commit('contragents/SET_CONTRAGENT', { creation_date: creationDate })
      },
      get () {
        return this.$store.state.contragents.detail.creation_date
      }
    },
    is_func: {
      set (isFunc) {
        this.$store.commit('contragents/SET_CONTRAGENT', { is_func: isFunc })
      },
      get () {
        return this.$store.state.contragents.detail.is_func
      }
    },
    okved: {
      set (okved) {
        this.$store.commit('contragents/SET_CONTRAGENT', { okved })
      },
      get () {
        return this.$store.state.contragents.detail.okved
      }
    },
    physical_address: {
      set (physicalAddress) {
        this.$store.commit('contragents/SET_CONTRAGENT', { physical_address: physicalAddress })
      },
      get () {
        return this.$store.state.contragents.detail.physical_address
      }
    },
    legal_address: {
      set (legalAddress) {
        this.$store.commit('contragents/SET_CONTRAGENT', { legal_address: legalAddress })
      },
      get () {
        return this.$store.state.contragents.detail.legal_address
      }
    },
    stat_value: {
      set (statValue) {
        this.$store.commit('contragents/SET_CONTRAGENT', { stat_value: statValue })
      },
      get () {
        return this.$store.state.contragents.detail.stat_value
      }
    },
    contract_accept_date: {
      set (contractAcceptDate) {
        this.$store.commit('contragents/SET_CONTRAGENT', { contract_accept_date: contractAcceptDate })
      },
      get () {
        return this.$store.state.contragents.detail.contract_accept_date
      }
    },
    current_date: {
      set (currentDate) {
        this.$store.commit('contragents/SET_CONTRAGENT', { current_date: currentDate })
      },
      get () {
        return this.$store.state.contragents.detail.current_date
      }
    },
    current_contract_date: {
      set (currentContractDate) {
        this.$store.commit('contragents/SET_CONTRAGENT', { current_contract_date: currentContractDate })
      },
      get () {
        return this.$store.state.contragents.detail.current_contract_date
      }
    },
    platform: {
      set (platform) {
        this.$store.commit('contragents/SET_CONTRAGENT', { platform })
      },
      get () {
        return this.$store.state.contragents.detail.platform
      }
    },
    norm_value: {
      set (normValue) {
        this.$store.commit('contragents/SET_CONTRAGENT', { norm_value: normValue })
      },
      get () {
        return this.$store.state.contragents.detail.norm_value
      }
    },
    number_contract: {
      set (numberContract) {
        this.$store.commit('contragents/SET_CONTRAGENT', { number_contract: numberContract })
      },
      get () {
        return this.$store.state.contragents.detail.number_contract
      }
    },
    signed_user: {
      set (signedUser) {
        this.$store.commit('contragents/SET_CONTRAGENT', { signed_user: signedUser })
      },
      get () {
        return this.$store.state.contragents.detail.signed_user
      }
    },
    current_user: {
      set (currentUser) {
        this.$store.commit('contragents/SET_CONTRAGENT', { current_user: currentUser })
      },
      get () {
        return this.$store.state.contragents.detail.current_user
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
