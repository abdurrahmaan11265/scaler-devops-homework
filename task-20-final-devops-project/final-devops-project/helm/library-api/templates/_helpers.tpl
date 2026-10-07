{{- define "lib.name" -}}{{ .Release.Name }}{{- end -}}
{{- define "lib.labels" -}}
app: {{ include "lib.name" . }}
app.kubernetes.io/name: library-api
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end -}}
