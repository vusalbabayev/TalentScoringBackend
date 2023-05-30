from django.contrib import admin
from app import models as model
from django.contrib.admin.widgets import AutocompleteSelect
from django.db import models
# Register your models here.


class AnswerTabularInline(admin.TabularInline):
    model = model.Answer
    fields = ('answer_title', 'answer_weight','answer_dependens_on','stage_fit')
    raw_id_fields = ('answer_dependens_on', 'stage_fit')
    fk_name = "question_id"


@admin.register(model.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title','stage', 'question_dependens_on_answer', 'question_type')
    inlines = [AnswerTabularInline]
    search_fields= ('question_title',)
    # autocomplete_fields = ['stage']
# 
    # 
# 
    # formfield_overrides = {
        # models.ForeignKey: {'widget': AutocompleteSelect}
    # }


@admin.register(model.Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'parent', 'slug', 'stage_index')
@admin.register(model.Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields= ('answer_title',)
    autocomplete_fields = ['answer_dependens_on']
    list_display = ('answer_title', 'question_id', 'answer_weight')

    # formfield_overrides = {
    #     models.ForeignKey: {'widget': AutocompleteSelect}
    # }
admin.site.register(model.UserAccount) 
