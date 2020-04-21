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
        v-toolbar(elevation="0")
          v-btn(icon class="hidden-xs-only" :to="'/contragent/' + $route.params.contragentId")
            v-icon mdi-arrow-left
          v-toolbar-title Пакет № {{ package.id }}
          v-spacer
          v-toolbar-items(class="hidden-sm-and-down" color="indigo" dark fixed)
            v-btn(
              v-if="packageActiveStatus"
              text
              tile
              class="custom-transform-class text-none"
              color="error"
              @click="DEACTIVATE_PACKAGE({ contragentId: package.contragent, packageId: package.id })"
            )
              | Сделать неактивным
            v-btn(
              v-if="packageActiveStatus"
              text
              tile
              class="ml-2 custom-transform-class text-none"
              color="primary"
              @click="REGENERATE_PACKAGE({ contragentId: package.contragent, packageId: package.id })"
            )
              | Перегенерировать
          v-menu
            template(v-slot:activator="{ on }")
              v-btn(
                class="hidden-md-and-up"
                icon
                v-on="on"
              )
                v-icon mdi-dots-vertical
            v-list
              v-list-item
                v-btn(
                  v-if="packageActiveStatus"
                  text
                  tile
                  outlined
                  class="custom-transform-class text-none"
                  color="error"
                  @click="DEACTIVATE_PACKAGE({ contragentId: package.contragent, packageId: package.id })"
                )
                  | Сделать неактивным
              v-list-item
                v-btn(
                  v-if="packageActiveStatus"
                  text
                  tile
                  outlined
                  class="ml-2 custom-transform-class text-none"
                  color="primary"
                  @click="REGENERATE_PACKAGE({ contragentId: package.contragent, packageId: package.id })"
                )
                  | Перегенерировать
        v-card-title(class="headline font-weight-light px-10")
        v-tabs(
          v-model="tab"
          background-color="transparent"
          color="primary"
          grow
        )
          v-tab(
            v-for="item in items"
            :key="item"
          )
            | {{ item }}
        v-tabs-items(v-model="tab")
          v-tab-item
            v-card(
              flat
            )
              v-data-table(
                :headers="headers"
                :items="package.single_files"
                :items-per-page="5"
                class="elevation-0"
              )
                template(v-slot:item.actions="{ item }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on }")
                      v-btn(
                        icon
                        v-on="on"
                        color="blue"
                        :href="item.file_path || ''"
                        target="_blank"
                      )
                        v-icon(small) mdi-download
                    span Скачать
          v-tab-item
            v-card(
              flat
            )
              v-data-table(
                :headers="headers"
                :items="package.pack_files['Акт']"
                :items-per-page="5"
                class="elevation-0"
              )
                template(v-slot:item.actions="{ item }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on }")
                      v-btn(
                        icon
                        v-on="on"
                        color="blue"
                        :href="item.file_path || ''"
                        target="_blank"
                      )
                        v-icon(small) mdi-download
                    span Скачать
          v-tab-item
            v-card(
              flat
            )
              v-data-table(
                :headers="headers"
                :items="package.pack_files['Счет']"
                :items-per-page="5"
                class="elevation-0"
              )
                template(v-slot:item.actions="{ item }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on }")
                      v-btn(
                        icon
                        v-on="on"
                        color="blue"
                        :href="item.file_path || ''"
                        target="_blank"
                      )
                        v-icon(small) mdi-download
                    span Скачать
          v-tab-item
            v-card(
              flat
            )
              v-data-table(
                :headers="headers"
                :items="package.pack_files['Счет-фактура']"
                :items-per-page="5"
                class="elevation-0"
              )
                template(v-slot:item.actions="{ item }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on }")
                      v-btn(
                        icon
                        v-on="on"
                        color="blue"
                        :href="item.file_path || ''"
                        target="_blank"
                      )
                        v-icon(small) mdi-download
                    span Скачать
          v-tab-item
            v-card(
              flat
            )
              v-data-table(
                :headers="headers"
                :items="otherFiles"
                :items-per-page="-1"
                class="elevation-0"
                hide-default-footer
              )
                template(v-slot:footer)
                  v-toolbar(flat color="white")
                    v-spacer
                    v-dialog(
                      v-model="packageDialogState"
                      persistent
                      max-width="600px"
                    )
                      template(v-slot:activator="{ on }")
                        v-btn(
                          text
                          tile
                          outlined
                          class="ml-2 custom-transform-class text-none"
                          color="primary"
                          v-on="on"
                        )
                          | Добавить файл
                      v-card(outlined)
                        v-card-title
                          span(class="headline") Добавление файла
                        v-card-text
                          v-container(px-0 pb-0)
                            v-row(no-gutters)
                              v-col(cols="12")
                                VueFileAgent(
                                  ref="vueFileAgent"
                                  v-model="filesDataForUpload"
                                  :theme="'list'"
                                  :maxFiles="1"
                                  :multiple="true"
                                  :deletable="true"
                                  :compact="true"
                                  :helpText="'Загрузите свой файл'"
                                  :errorText="{ type: 'Некоректный тип файла. Доступно только xlsx', size: 'Размер файла выше 2MB' }"
                                  @delete="fileDeleted($event)"
                                )
                                small *Файл должен быть с расширением .xlsx и размером меньше двух мегабайт
                        v-card-actions
                          v-spacer
                          v-btn(color="blue darken-1" text @click="packageDialogState = false") Закрыть
                          v-btn(color="blue darken-1" text @click="upload") Отправить
                template(v-slot:item.actions="{ item }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on }")
                      v-btn(
                        icon
                        v-on="on"
                        color="blue"
                        :href="item.file_path || ''"
                        target="_blank"
                      )
                        v-icon(small) mdi-download
                    span Скачать
                  v-dialog(v-model="packageFileWarningDialog" persistent max-width="290")
                    template(v-slot:activator="{ on: dialog }")
                      v-tooltip(bottom)
                        template(v-slot:activator="{ on: tooltip }")
                          v-btn(
                            icon
                            v-on="{ ...dialog, ...tooltip }"
                            color="red"
                          )
                            v-icon(small) mdi-download
                        span Удалить
                    v-card
                      v-card-title(class="headline") Use Google's location service?
                      v-card-text Let Google help apps determine location. This means sending anonymous location data to Google, even when no apps are running.
                      v-card-actions
                        v-spacer
                        v-btn(color="green darken-1" text @click="packageFileWarningDialog = false") Disagree
                        v-btn(color="green darken-1" text @click="deleteFile(item)") Agree
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { ValidationProvider, ValidationObserver } from 'vee-validate'

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  async asyncData ({ $axios, store, params }) {
    await store.dispatch('packages/FETCH_PACKAGE', { contragentId: params.contragentId, packageId: params.packageId })
    await store.dispatch('files/FETCH_FILES', { contragentId: params.contragentId, packageId: params.packageId })
  },
  data: () => ({
    packageDialogState: false,
    packageFileWarningDialog: false,
    filesDataForUpload: null,
    tab: null,
    headers: [
      {
        text: 'Номер',
        align: 'center',
        sortable: false,
        value: 'id'
      },
      { text: 'Имя', value: 'file_name' },
      { text: 'Дата создания', value: 'creation_date' },
      { text: 'Действия', value: 'actions', align: 'center', sortable: false }
      // Дата последнего платежа
      // Ответственное лицо
    ],
    items: [
      'Основные файлы', 'Акты', 'Счета', 'Счета фактур', 'Другие файлы'
    ],
    menu: [
      { icon: 'home', title: 'Link A' },
      { icon: 'info', title: 'Link B' },
      { icon: 'warning', title: 'Link C' }
    ]
  }),
  computed: {
    ...mapState({
      package: state => state.packages.detail,
      packageActiveStatus: state => state.packages.detail.is_active,
      otherFiles: state => state.files.list
    })
  },
  methods: {
    ...mapActions({
      REGENERATE_PACKAGE: 'packages/REGENERATE_PACKAGE',
      DEACTIVATE_PACKAGE: 'packages/DEACTIVATE_PACKAGE',
      DELETE_FILE: 'files/DELETE_FILE'
    }),
    upload () {
      this.$store.dispatch('files/CREATE_FILE', {
        vueFileAgent: this.$refs.vueFileAgent,
        contragentId: this.$route.params.contragentId,
        packageId: this.$route.params.packageId,
        filesDataForUpload: this.filesDataForUpload
      })
      this.packageDialogState = false
      this.filesDataForUpload = null
    },
    deleteFile (item) {
      this.DELETE_FILE({
        contragentId: this.$route.params.contragentId,
        packageId: this.$route.params.packageId,
        fileId: item.id
      })
      this.packageFileWarningDialog = false
    },
    fileDeleted (fileData) {
      this.filesDataForUpload = null
    }
  }
}
</script>
