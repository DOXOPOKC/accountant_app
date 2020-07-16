<template lang="pug">
  v-row(
    class="fill-height"
    justify="center"
    align="start"
    no-gutters
  )
    v-col(
      class="fill-height"
      xs12
      sm8
      md6
    )
      v-card(
        class="fill-height"
        flat
        exact
      )
        v-card-text(class="pa-0")
          v-data-table(
            :headers="headers"
            :items="contragents"
            item-key="id"
            class="elevation-0"
            sort-by="id"
            disable-pagination
            disable-filtering
            calculate-widths
            hide-default-footer
            show-expand
            single-expand
            :expanded.sync="expanded"
            @click:row="clicked"
          )
            template(v-slot:top)
              v-toolbar(flat)
                v-toolbar-title(class="headline font-weight-light") Контрагенты
                v-spacer
                v-btn(
                  v-if="!!excelTemplateLink"
                  outlined
                  class="mt-2 mr-2 text-none"
                  color="primary"
                  :href="excelTemplateLink"
                  target="_blank"
                ) Скачать Excel
                v-btn(
                  outlined
                  class="mt-2 text-none"
                  color="primary"
                  @click="contragentDialogState = true"
                ) Добавить контрагента
            template(v-slot:expanded-item="{ headers, item }")
              td(:colspan="headers.length" class="pa-0 ma-0")
                v-card(flat tile)
                  v-card-title(v-if="Object.keys(item.pack).length > 0" class="font-weight-light") Последний пакет:
                  v-card-text(v-if="Object.keys(item.pack).length > 0")
                    v-list-item(three-line)
                      v-list-item-content
                        v-list-item-title(class="font-weight-light") Пакет №{{ item.pack.id }}
                        v-list-item-subtitle() Дата создания: {{ item.pack.creation_date }}
                        v-list-item-subtitle() Статус - {{ item.pack.package_state.name_state }}
                  v-card-title(
                    v-else
                    class="font-weight-light"
                  ) Пакет отсутствует
                  v-card-actions
                    v-spacer
                    v-btn(
                      outlined
                      class="text-none"
                      color="primary"
                      :to="'contragent/' + item.id + '/'"
                    ) Перейти
              //- td(:colspan="headers.length") More info about {{ item.id }}
              //-   nuxt-link(tag="tr" :to="'contragent/' + item.id + '/'") {{ item.pack}}
      v-dialog(v-model="contragentDialogState" persistent max-width="600px")
        v-card(outlined)
          v-card-title
            span(class="headline") Добавление контрагента
          v-card-text
            v-container(px-0 pb-0)
              v-row(no-gutters)
                v-col(cols="12")
                  VueFileAgent(
                    ref="vueFileAgent"
                    v-model="filesDataForUpload"
                    :theme="'list'"
                    :accept="'.xlsx'"
                    :maxSize="'2MB'"
                    :maxFiles="1"
                    :multiple="true"
                    :deletable="true"
                    :compact="true"
                    :helpText="'Загрузите свой файл'"
                    :errorText="{ type: 'Некоректный тип файла. Доступно только xlsx', size: 'Размер файла выше 2MB' }"
                    @select="upload($event)"
                    @delete="fileDeleted($event)"
                  )
                  small *Файл должен быть с расширением .xlsx и размером меньше двух мегабайт
          v-card-actions
            v-spacer
            v-btn(color="blue darken-1" text @click="contragentDialogState = false") Закрыть
            v-btn(color="blue darken-1" text @click="upload") Отправить
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { types } from '~/store/contragents'

export default {
  async asyncData ({ $axios, store, params, app }) {
    await store.dispatch(`contragents/${types.FETCH_CONTRAGENTS}`, app)
  },
  data: () => ({
    expanded: [],
    uploaded: false,
    filesDataForUpload: null,
    uploadUrl: 'http://localhost/api/contragents/',
    contragentDialogState: false,
    headers: [
      { text: '', value: 'id' },
      {
        text: 'Название',
        align: 'left',
        sortable: false,
        value: 'excell_name'
      },
      { text: 'Факт. адрес', value: 'physical_address' },
      { text: 'Класс', value: 'klass' },
      { text: 'ИНН', value: 'inn' },
      { text: 'Задолжность', value: 'debt' },
      { text: '', value: 'data-table-expand' }
    ]
  }),
  computed: {
    ...mapState({
      contragents: state => state.contragents.list,
      excelTemplateLink: state => state.contragents.excelTemplateLink
    })
  },
  methods: {
    ...mapActions([types.FETCH_CONTRAGENTS]),
    clicked (value) {
      if (!this.expanded.includes(value)) {
        this.expanded = [value]
      } else {
        this.expanded = []
      }
    },
    upload () {
      this.$store.dispatch('contragents/CREATE_CONTRAGENT', {
        vueFileAgent: this.$refs.vueFileAgent,
        uploadUrl: this.uploadUrl,
        uploadHeaders: this.uploadHeaders,
        filesDataForUpload: this.filesDataForUpload
      })
      this.contragentDialogState = false
      this.filesDataForUpload = null
    },
    fileDeleted (fileData) {
      this.filesDataForUpload = null
    }
  }
}
</script>
