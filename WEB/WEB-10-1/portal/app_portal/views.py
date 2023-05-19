from django.shortcuts import render, redirect
from .forms import AuthorForm, TagForm, QuoteForm
from .models import Author, Tag, Quote


def main(request):
    quotes = Quote.objects.all()
    return render(request, 'app_portal/index.html', context={"title": quotes, "quotes": quotes})


def author(request):
    form = AuthorForm(instance=Author())
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='app_portal:root')
        else:
            return render(request, 'app_portal/author.html', {'form': form})
    return render(request, 'app_portal/author.html', context={"title": "Author", "form":form})


def tag(request):
    form = TagForm(instance=Tag())
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='app_portal:root')
        else:
            return render(request, 'app_portal/tag.html', {'form': form})
    return render(request, 'app_portal/tag.html', context={"title": "Tag", "form":form})


def quote(request):
    form = QuoteForm(instance=Quote())
    authors = Author.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_authors = Author.objects.filter(full_name__in=request.POST.getlist('authors'))
            for author in choice_authors.iterator():
                new_quote.authors.add(author)

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='app_portal:root')
        else:
            return render(request, 'app_portal/quote.html', {"authors": authors, "tags": tags, 'form': form})

    return render(request, 'app_portal/quote.html', {"authors": authors, "tags": tags, 'form': QuoteForm()})


def author_details(request, author_id):
    author = Author.objects.get(id=author_id)

    return render(request, 'app_portal/author_details.html', {"author": author})
