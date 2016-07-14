{%- extends 'null.tpl' -%}

{% block header %}
// Spark scala application
{% endblock header %}

{% block in_prompt %}
// In[{{ cell.execution_count if cell.execution_count else ' ' }}]:
{% endblock in_prompt %}

{% block input %}
{{ cell.source }}
{% endblock input %}

{% block markdowncell scoped %}
{{ cell.source | comment_lines('//') }}
{% endblock markdowncell %}