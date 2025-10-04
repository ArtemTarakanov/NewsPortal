from django import template

register = template.Library()

@register.filter()
def rating_color(value):

    if value > 0:
        return "text-success"  # зеленый цвет для положительного
    elif value < 0:
        return "text-danger"   # красный цвет для отрицательного
    else:
        return "text-muted"    # серый цвет для нулевого

@register.filter()
def rating_label(value, label_type='color'):

    if label_type == 'text':
        if value > 0:
            return "👍 Положительный"
        elif value < 0:
            return "👎 Отрицательный"
        else:
            return "⚪ Нейтральный"
    elif label_type == 'icon':
        if value > 0:
            return "📈"
        elif value < 0:
            return "📉"
        else:
            return "➖"
    else:
        # По умолчанию возвращаем цвет (как в rating_color)
        return rating_color(value)
    
@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError
    
    bad_words = ['редиска', 'плохой', 'нехороший', 'дурак']

    for word in bad_words:
        censored_word = word[0] + '*' * (len(word) - 1)
        value = value.replace(word, censored_word)
        value = value.replace(word.capitalize(), censored_word)
        
    return value