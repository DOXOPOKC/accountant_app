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
          ValidationObserver(
            ref="form"
            v-slot="{ passes }"
          )
            form(@submit.prevent="passes(onSubmit)")
              v-expansion-panels(
                :value="panels"
                accordion
                multiple
                hover
                flat
                tile
              )
                v-expansion-panel(
                  v-for="(item, i) in contragentInfo"
                  :key="i"
                )
                  v-expansion-panel-header {{ Object.keys(item)[0] }}
                  v-expansion-panel-content
                    //- ValidationProvider(
                    //-   rules="required"
                    //-   v-slot="{ errors }"
                    //- )
                    v-text-field(
                      v-if="klass"
                      v-model="klass"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="excell_name"
                      v-model="excell_name"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="dadata_name"
                      v-model="dadata_name"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="debt"
                      v-model="debt"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="inn"
                      v-model="inn"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="ogrn"
                      v-model="ogrn"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="kpp"
                      v-model="kpp"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="rs"
                      v-model="rs"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="ks"
                      v-model="ks"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="bank"
                      v-model="bank"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="bik"
                      v-model="bik"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="opf"
                      v-model="opf"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="director_status"
                      v-model="director_status"
                      :label="Object.values(item)[0]"
                    )
                    v-text-field(
                      v-else-if="director_name"
                      v-model="director_name"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="creation_date"
                      v-model="creation_date"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="is_func"
                      v-model="is_func"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="okved"
                      v-model="okved"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="physical_address"
                      v-model="physical_address"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="legal_address"
                      v-model="legal_address"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="stat_value"
                      v-model="stat_value"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="contract_accept_date"
                      v-model="contract_accept_date"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="current_date"
                      v-model="current_date"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="current_contract_date"
                      v-model="current_contract_date"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="platform"
                      v-model="platform"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="norm_value"
                      v-model="norm_value"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="number_contract"
                      v-model="number_contract"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="signed_user"
                      v-model="signed_user"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else-if="current_user"
                      v-model="current_user"
                      :label="Object.values(item)[0]"

                    )
                    v-text-field(
                      v-else
                      v-model="test"
                      :label="Object.values(item)[0]"

                    )
        v-card-actions(class="px-10 py-6")
          //- v-btn(
          //-   color="primary"
          //-   @click=""
          //-   to="put /contragents/{id}/packages/{package_id}"
          //- )
          //-   | Перегенерировать
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
    test: null,
    id: 1,
    klass: 1,
    excell_name: 'СТРОИТЕЛЬНАЯ КОМПАНИЯ ПГС',
    dadata_name: 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ ',
    debt: 0,
    inn: 4214032864,
    ogrn: 1114214000119,
    kpp: 421401001,
    rs: null,
    ks: null,
    bank: null,
    bik: null,
    opf: null,
    director_status: 'директор',
    director_name: 'Чамин Роман Иванович',
    creation_date: '2011-02-17',
    is_func: true,
    okved: '41.20',
    physical_address: '652873, ОБЛАСТЬ КЕМЕРОВСКАЯ ОБЛАСТЬ - КУЗБАСС, ГОРОД МЕЖДУРЕЧЕНСК, ПРОЕЗД ГОРЬКОГО, ДОМ 4Б',
    legal_address: '652873, ОБЛАСТЬ КЕМЕРОВСКАЯ ОБЛАСТЬ - КУЗБАСС, ГОРОД МЕЖДУРЕЧЕНСК, ПРОЕЗД ГОРЬКОГО, ДОМ 4Б',
    stat_value: 100,
    contract_accept_date: '2018-07-01',
    current_date: '2020-02-11',
    current_contract_date: '2020-02-11',
    platform: null,
    norm_value: 44,
    number_contract: 1,
    signed_user: null,
    current_user: null
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
      }
    }),
    contragent: {
      get () {
        return this.$store.state.contragents.detail
      },
      set (newValue) {}
    },
    panels () {
      return [...Array(this.contragentInfo.length).keys()]
    }
  },
  methods: {
    ...mapActions({
      UPDATE_CONTRAGENT: 'contragents/UPDATE_CONTRAGENT',
      GENERATE_PACKAGE: 'packages/GENERATE_PACKAGE'
    }),
    foo () {
      this.UPDATE_CONTRAGENT({
        id: this.id,
        klass: this.klass,
        excell_name: this.excell_name,
        dadata_name: this.dadata_name,
        debt: this.debt,
        inn: this.inn,
        ogrn: this.ogrn,
        kpp: this.kpp,
        rs: this.rs,
        ks: this.ks,
        bank: this.bank,
        bik: this.bik,
        opf: this.opf,
        director_status: this.director_status,
        director_name: this.director_name,
        creation_date: this.creation_date,
        is_func: this.is_func,
        okved: this.okved,
        physical_address: this.physical_address,
        legal_address: this,
        stat_value: this,
        contract_accept_date: this,
        current_date: this,
        current_contract_date: this,
        platform: this,
        norm_value: this,
        number_contract: this,
        signed_user: this,
        current_user: this
      })
    },
    bar () {}
  }
}
</script>
