const BASE_URL = "http://127.0.0.1:5000";


// =========================================
// AUTO LOGIN CHECK
// =========================================

const currentUser =
    JSON.parse(localStorage.getItem("smarteval_user"));

if (currentUser) {

    // If already logged in and on landing/login page, redirect to dashboard
    if (
        window.location.pathname.includes("index.html") ||
        window.location.pathname.includes("login.html")
    ) {

        if (currentUser.role === "faculty") {

            window.location.href =
                "faculty-dashboard.html";

        } else {

            window.location.href =
                "student-dashboard.html";
        }
    }

} else {

    // Not logged in — protect dashboard pages
    const protectedPages = [
        "student-dashboard.html",
        "faculty-dashboard.html",
        "create-assignment.html",
        "upload-test.html"
    ];

    const onProtectedPage = protectedPages.some(page =>
        window.location.pathname.includes(page)
    );

    if (onProtectedPage) {

        alert("Please login first.");

        window.location.href = "login.html";
    }
}


// =========================================
// LOGOUT FUNCTION
// =========================================

function logout() {

    localStorage.removeItem("smarteval_user");

    window.location.href = "login.html";
}


// =========================================
// CHECK AUTH
// =========================================

function checkAuth(requiredRole = null) {

    const user =
        JSON.parse(localStorage.getItem("smarteval_user"));

    if (!user) {

        alert("Please login first");

        window.location.href = "login.html";

        return false;
    }

    if (
        requiredRole &&
        user.role !== requiredRole
    ) {

        alert(`Unauthorized Access. Please login as ${requiredRole}.`);

        window.location.href = "login.html";

        return false;
    }

    return user;
}


// =========================================
// GET USER
// =========================================

function getCurrentUser() {

    return JSON.parse(
        localStorage.getItem("smarteval_user")
    );
}


// =========================================
// FORMAT DATE
// =========================================

function formatDate(dateString) {

    if (!dateString) {

        return "No Deadline";
    }

    const date = new Date(dateString);

    return date.toLocaleDateString();
}


// =========================================
// API HELPER
// =========================================

async function apiRequest(

    endpoint,

    method = "GET",

    body = null,

    isFormData = false

) {

    const options = {

        method
    };

    if (body) {

        if (isFormData) {

            options.body = body;

        } else {

            options.headers = {

                "Content-Type": "application/json"
            };

            options.body = JSON.stringify(body);
        }
    }

    const response = await fetch(

        `${BASE_URL}${endpoint}`,

        options
    );

    return response.json();
}


// =========================================
// SHOW MESSAGE
// =========================================

function showMessage(

    elementId,

    message,

    type = "success"

) {

    const element =
        document.getElementById(elementId);

    if (!element) return;

    element.textContent = message;

    element.style.display = "block";

    if (type === "success") {

        element.style.background = "#1D2A1D";

        element.style.color = "#7CFC98";

    } else {

        element.style.background = "#2A1D1D";

        element.style.color = "#FC7C7C";
    }

    setTimeout(() => {

        element.style.display = "none";

    }, 4000);
}


// =========================================
// LOAD ASSIGNMENTS
// =========================================

async function loadAssignments() {

    try {

        const data = await apiRequest(

            "/get-assignments"
        );

        return data.assignments || [];

    } catch(error) {

        console.error(error);

        return [];
    }
}


// =========================================
// LOAD SUBMISSIONS
// =========================================

async function loadSubmissions() {

    try {

        const data = await apiRequest(

            "/get-submissions"
        );

        return data.submissions || [];

    } catch(error) {

        console.error(error);

        return [];
    }
}


// =========================================
// CREATE ASSIGNMENT
// =========================================

async function createAssignment(formData) {

    return await apiRequest(

        "/create-assignment",

        "POST",

        formData,

        true
    );
}


// =========================================
// SUBMIT ASSIGNMENT
// =========================================

async function uploadSubmission(formData) {

    return await apiRequest(

        "/upload-submission",

        "POST",

        formData,

        true
    );
}


// =========================================
// EVALUATE SUBMISSION
// =========================================

async function evaluateSubmission(submissionId) {

    return await apiRequest(

        `/evaluate-submission/${submissionId}`
    );
}


// =========================================
// LOGIN
// =========================================

async function login(email, password) {

    return await apiRequest(

        "/login",

        "POST",

        {

            email,
            password
        }
    );
}


// =========================================
// REGISTER STUDENT
// =========================================

async function registerStudent(payload) {

    return await apiRequest(

        "/register-student",

        "POST",

        payload
    );
}


// =========================================
// REGISTER FACULTY
// =========================================

async function registerFaculty(payload) {

    return await apiRequest(

        "/register-faculty",

        "POST",

        payload
    );
}
