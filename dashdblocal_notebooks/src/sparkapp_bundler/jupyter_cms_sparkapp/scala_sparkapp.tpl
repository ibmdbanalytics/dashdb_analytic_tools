{# (c) Copyright IBM Corporation 2016
 # LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause}

{%- extends 'null.tpl' -%}

{% block header %}

// Spark scala application

import org.apache.spark._
import org.apache.spark.sql._

object SampleApp {
  def main(arguments: Array[String]) {

    val sparkConf = new SparkConf().setAppName("SampleApp")
    val sc = new SparkContext(sparkConf)
    val sqlContext = SQLContext.getOrCreate(sc)

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

{% block footer %}
  }
}
{% endblock footer %}
