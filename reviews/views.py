from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import PublisherForm, SearchForm, ReviewForm, ContributorForm
from .models import Book, Contributor, Publisher, Review
from .utils import average_rating
from django.utils import timezone


def index(request):
    return render(request, "base.html")


def book_search(request):
    books = set()
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    if form.is_valid():
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        else:
            first_name_contributors = Contributor.objects.filter(
                first_names__icontains=search
            )

            for contributor in first_name_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

            last_name_contributors = Contributor.objects.filter(
                last_names__icontains=search
            )

            for contributor in last_name_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

        return render(
            request, "reviews/search_results.html",
            {"form": form, "search_text": search_text, "books": books},
        )


def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({'book': book, 'book_rating': book_rating, 'number_of_reviews': number_of_reviews})
    context = {'book_list': book_list}
    return render(request, 'reviews/book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        number_of_reviews = len(reviews)
    else:
        book_rating = None
        number_of_reviews = 0
    context = {
        'book': book,
        'book_rating': book_rating,
        'number_of_reviews': number_of_reviews,
        'reviews': reviews
    }
    return render(request, 'reviews/book_detail.html', context)


def publisher_edit(request, pk=None):
    if pk is not None:  # Chỉnh sửa null
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None
    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, 'Publisher "{}" was created.'.format(updated_publisher))
            else:
                messages.success(request, 'Publisher "{}" was updated.'.format(updated_publisher))
        return redirect("publisher_edit", updated_publisher.pk)
    else:  # request.method == GET
        form = PublisherForm(instance=publisher)
    return render(
        request,
        "reviews/instance-form.html",
        {
            "form": form,
            "model_type": "Publisher",
            "instance": publisher,
        },
    )


def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)

    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(False)
            updated_review.book = book

            if review is None:
                messages.success(request, 'Review for "{}" created.'.format(book))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, 'Review for "{}" updated.'.format(book))

            updated_review.save()
            return redirect("book_detail", book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/instance-form.html",
        {
            "form": form,
            "instance": review,
            "model_type": "Review",
            "related_instance": book,
            "related_model_type": "Book",
        },
    )


def contributor_edit(request, pk=None):
    if pk is not None:  # Chỉnh sửa null
        contributor = get_object_or_404(Contributor, pk=pk)
    else:
        contributor = None
    if request.method == "POST":
        form = ContributorForm(request.POST, instance=contributor)
        if form.is_valid():
            updated_contributor = form.save()
            if contributor is None:
                messages.success(request, 'Contributor "{}" was created.'.format(updated_contributor))
            else:
                messages.success(request, 'Contributor "{}" was updated.'.format(updated_contributor))
        return redirect("contributor_edit", updated_contributor.pk)
    else:  # request.method == GET
        form = ContributorForm(instance=contributor)
    return render(
        request,
        "reviews/instance-form.html",
        {
            "form": form,
            "model_type": "Contributor",
            "instance": contributor,
        },
    )
