workspace "Intiva" "Intiva Platform — Vehicle Loans Simulator" {

    model {
        client = person "Client" \
            "Person that seeks information about vehicle loans (bank, efective rate)."

        twilio = softwareSystem "Twilio" \
            "Delivers outbound email notifications to clients with its simulations." \
            "External"

        oauth2 = softwareSystem "OAuth2" \
            "Handles federated authentication and issues JWT tokens via the OAuth2 / OpenID Connect protocol." \
            "External"

        intiva = softwareSystem "Intiva Platform" \
            "Application that serves a vehicle loan simulator using relevant variables like the capital, rate and time." {

            mobileApp = container "Intiva Mobile Application" \
                "Cross-platform application for vehicle loans simulation." \
                "Dart, Flutter" \
                "MobileApp" {
                mobileIamContext = component "IAM UI" \
                    "Displays the sign-in and sign-up forms." \
                    "Dart, Flutter"

                mobileProfilesContext = component "Profiles UI" \
                    "Displays user's personal information." \
                    "Dart, Flutter"

                mobileVehiclesContext = component "Vehicles UI" \
                    "Displays available vehicles for possible simulations." \
                    "Dart, Flutter"

                mobileAnalyticsContext = component "Analytics UI" \
                    "Displays simulation form and simulation results." \
                    "Dart, Flutter"

                mobileShared = component "Shared" \
                    "Handles common utilities and widgets across the contexts." \
                    "Dart, Flutter"
            }

            webServices = container "Intiva Cloud API" \
                "Monolithic API exposing a versioned REST API. Also handles all business logic, authentication delegation, and integration with external services." \
                "Python 3.14, FastAPI" \
                "API" {
                apiCommunicationContext = component "Communication" \
                    "Manages notifications of loans simulations." \
                    "Python 3.14, FastAPI"

                apiIamContext = component "Identity and Access Management" \
                    "Manages user authentication and authorization." \
                    "Python 3.14, FastAPI"

                apiProfilesContext = component "Profiles and Preferences" \
                    "Manages personal information and preferences." \
                    "Python 3.14, FastAPI"

                apiVehiclesContext = component "Vehicle Management" \
                    "Manages vehicle information and registration for loan simulations." \
                    "Python 3.14, FastAPI"

                apiAnalyticsContext = component "Analytics" \
                    "Manages vehicle loan simulation operations." \
                    "Python 3.14, FastAPI"

                apiShared = component "Shared" \
                    "Handles common infrastructure, implementations and value objects across the contexts." \
                    "Python 3.14, FastAPI"
            }

            database = container "Intiva MySQL Database" \
                "Table store for all structured domain data including users, vehicles and loan simulations." \
                "MySQL" \
                "Database"

            localDatabase = container "Mobile SQLite Database" \
                "Stores app data locally on the mobile device." \
                "SQLite" \
                "Database"
        }

        client         -> intiva         "Simulates vehicle loans"
        client         -> mobileApp      "Simulates vehicle loans"
        intiva         -> twilio         "Sends SMS and email notifications"          "HTTPS"
        intiva         -> oauth2         "Delegates authentication"                   "HTTPS/OIDC"
        mobileApp      -> webServices    "Reads from and writes loan simulation data" "JSON/HTTPS"
        mobileApp      -> localDatabase  "Caches and retrieves simulation data"
        webServices    -> database       "Reads from and writes to"                   "MongoDB Wire Protocol"
        webServices    -> twilio         "Sends notifications via"                    "HTTPS"
        webServices    -> oauth2         "Validates tokens with"                      "HTTPS/OIDC"

        apiIamContext           -> oauth2        "Requests authorization from Google"  "HTTPS"
        apiIamContext           -> apiShared     "Uses shared utilities"
        apiIamContext           -> database      "Stores user data"                    "MongoDB Wire Protocol"
        apiVehiclesContext      -> apiIamContext "Verifies JWT and ensures the roles of the user"
        apiVehiclesContext      -> database      "Stores vehicle data"                 "MongoDB Wire Protocol"
        apiVehiclesContext      -> apiShared     "Uses shared utilities"
        apiCommunicationContext -> twilio        "Sends notifications via"             "HTTPS"
        apiProfilesContext      -> database      "Stores user's personal data"         "MongoDB Wire Protocol"
        apiProfilesContext      -> apiIamContext "Verifies JWT"
        apiProfilesContext      -> apiShared     "Uses shared utilities"
        apiAnalyticsContext     -> database      "Stores loan simulation data"         "MongoDB Wire Protocol"
        apiAnalyticsContext     -> apiIamContext "Verifies JWT"
        apiAnalyticsContext     -> apiCommunicationContext "Sends data to report to the user email" "ACL"
        apiAnalyticsContext     -> apiShared     "Uses shared utilities"

        mobileIamContext        -> webServices   "Authenticates mobile users"              "JSON/HTTPS"
        mobileIamContext        -> mobileShared  "Extends base api and endpoint and widget utilities"
        mobileIamContext        -> oauth2        "Redirects to authorization page from Google"      "HTTPS"
        mobileProfilesContext   -> webServices   "Requests personal information"           "JSON/HTTPS"
        mobileProfilesContext   -> mobileShared  "Extends base api and endpoint and widget utilities"
        mobileVehiclesContext   -> webServices   "Requests available vehicles to simulate" "JSON/HTTPS"
        mobileVehiclesContext   -> mobileShared  "Extends base api and endpoint and widget utilities"
        mobileAnalyticsContext  -> webServices   "Requests and registers loan simulation data" "JSON/HTTPS"
        mobileAnalyticsContext  -> mobileShared  "Extends base api and endpoint and widget utilities"
        mobileAnalyticsContext  -> localDatabase "Caches registered loan simulations"

        deploymentEnvironment "Production" {

            deploymentNode "Azure App Service" "Cloud platform where the backend service is deployed and executed." "Azure App Service / Docker" {
                deploymentNode "Intiva Web Service" "Backend API service for algorithm executing." "Azure App Service / Docker" {
                    containerInstance webServices
                }
            }

            deploymentNode "MongoDB Atlas" "Managed cloud database service used by the backend." "Azure Database Service" {
                deploymentNode "Intiva Database" "Managed MySQL database used by Intiva Platform." "Azure Database Cluster" {
                    containerInstance database
                }
            }

            deploymentNode "Firebase App Distribution" "End-user smartphone or tablet used to access the mobile app." "Firebase App Distribution" {
                deploymentNode "Intiva Mobile Application" "Cross-platform mobile app deployed on cloud in FireBase App Distribution." "Firebase App Distribution" {
                    containerInstance mobileApp
                }

                deploymentNode "Mobile Local Database" "Local database stored on the mobile device." "SQLite on-device storage" {
                    containerInstance localDatabase
                }
            }
        }
    }

    configuration {
        Scope softwaresystem
    }

    views {
        systemContext intiva "SystemContext" {
            include *
            autoLayout lr
            title "Intiva Platform — Software Architecture Context Diagram"
        }

        container intiva "Containers" {
            include *
            autoLayout lr
            title "Intiva Platform — Software Architecture Container Diagram"
        }

        deployment intiva "Production" "ProductionDeployment" {
            include *
            autoLayout lr 100 100 90
            title "Intiva Platform - Software Architecture Deployment Diagram"
        }

        component mobileApp "MobileComponent" {
            include *
            autoLayout lr
            title "Intiva Platform — Software Architecture Mobile App Component Diagram"
        }

        component webServices "WebServicesAppComponent" {
            include *
            autoLayout lr
            title "Intiva Platform — Software Architecture Cloud Platform Component Diagram"
        }

        styles {
            element "Person" {
                shape Person
                background #1f4e79
                color #ffffff
            }
            element "Software System" {
                background #7F77DD
                color #ffffff
            }
            element "External" {
                background #888780
                color #ffffff
            }
            element "Frontend" {
                shape "WebBrowser"
            }
            element "Container" {
                background #534AB7
                color #ffffff
            }
            element "Database" {
                shape Cylinder
                background #BA7517
                color #ffffff
            }
            element "MobileApp" {
                shape MobileDevicePortrait
                background #1D9E75
                color #ffffff
            }
            element "API" {
                shape Box
                background #2B14FA
                color #ffffff
            }
        }
    }
}