from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Problem, Submission

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, "problems/problem_list.html", {"problems": problems})

@login_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    if request.method == 'POST':
        code = request.POST['code']
        language = request.POST['language']
        Submission.objects.create(
            user=request.user,
            problem=problem,
            code=code,
            language=language,
            verdict="Pending"
        )
        messages.success(request, "Your submission was received! Verdict: Pending")
        return redirect('problem_detail', problem_id=problem_id)

    return render(request, "problems/problem_detail.html", {"problem": problem})

@login_required
def my_submissions(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'problems/my_submissions.html', {'submissions': submissions})

from django.shortcuts import render, get_object_or_404
from .models import Problem
from .utils import run_code  # Assuming you placed your docker runner here
from django.views.decorators.csrf import csrf_exempt
from .models import Problem, Submission

@csrf_exempt
@login_required
def run_submission(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)

    if request.method == "POST":
        code = request.POST.get("code")
        language = "py"  # Hardcoded since you're using Python

        all_passed = True
        results = []

        for test in problem.testcases.all():
            output = run_code(code, test.input_data)
            passed = output.strip() == test.expected_output.strip()
            results.append({
                "input": test.input_data,
                "expected": test.expected_output,
                "actual": output.strip(),
                "passed": passed
            })
            if not passed:
                all_passed = False

        # Create submission entry here
        Submission.objects.create(
            user=request.user,
            problem=problem,
            code=code,
            language=language,
            verdict="Accepted" if all_passed else "Wrong Answer"
        )

        return render(request, "problems/run_result.html", {
            "problem": problem,
            "code": code,
            "results": results
        })
