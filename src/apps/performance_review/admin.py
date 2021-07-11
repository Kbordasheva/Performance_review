from django.contrib import admin

from performance_review.models import PerformanceReview, Goal, Criteria, Comment


class GoalsInline(admin.TabularInline):
    model = Goal
    fk_name = 'review'
    extra = 0


class CriteriaInline(admin.TabularInline):
    model = Criteria
    fk_name = 'goal'
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    fk_name = 'goal'
    extra = 0


class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'employee')
    fields = ('year',
              'employee',
              )

    inlines = [GoalsInline, ]


class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'is_done', 'created_at', 'updated_at',)
    fields = ('review',
              'text',
              'is_done',
              'created_at',
              'updated_at',
              )
    readonly_fields = ('created_at', 'updated_at')

    inlines = [CriteriaInline, CommentInline]


class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'goal',
                    'text',
                    'is_done',
                    'start_date',
                    'deadline',
                    'finish_date',
                    'created_at',
                    'updated_at',
                    )
    fields = ('goal',
              'text',
              'is_done',
              'start_date',
              'deadline',
              'finish_date',
              'created_at',
              'updated_at',
              )

    readonly_fields = ('created_at', 'updated_at')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'created_at', 'updated_at')
    fields = ('author',
              'text',
              'goal',
              'created_at',
              'updated_at',
              )
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(PerformanceReview, PerformanceReviewAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Criteria, CriteriaAdmin)
admin.site.register(Comment, CommentAdmin)

