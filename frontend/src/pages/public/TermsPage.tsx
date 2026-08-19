import { Link } from 'react-router-dom'

const section = 'mb-8'
const heading = 'text-xl font-bold text-gray-900 mb-3'
const sub = 'text-sm text-gray-600 leading-relaxed'
const list = 'list-disc list-inside text-sm text-gray-600 leading-relaxed space-y-1'

const TermsPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="card !p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Terms &amp; Conditions</h1>
            <p className="text-sm text-gray-500">
              Effective date: 7 August 2026 · Version 1.0 · Jurisdiction: Republic of Kenya
            </p>
            <p className="text-sm text-gray-600 mt-3 leading-relaxed">
              By accessing the N.O.U. Digital Systems website, creating an account, submitting
              information, requesting a software development service, purchasing or accessing a
              product, downloading software, participating in an assessment, or otherwise using an
              N.O.U. service, you acknowledge that you have read, understood, and agreed to these
              Terms. The full policy set is maintained in the company&apos;s{' '}
              <code className="text-xs bg-gray-100 px-1 py-0.5 rounded">policies.md</code>.
            </p>
          </div>

          <div className={section}>
            <h2 className={heading}>1. Customer Terms and Conditions</h2>
            <p className={sub}>
              <strong>Acceptance.</strong> Additional terms may apply to specific products, services,
              projects, subscriptions, software licences, or employment applications. Where
              additional terms conflict with these general Terms, the specific written agreement
              applies to that transaction.
            </p>
            <ul className={list + ' mt-3'}>
              <li><strong>Eligibility:</strong> you must be at least 18 years old where a service requires it and provide accurate, truthful information. N.O.U. may set additional eligibility requirements per service.</li>
              <li><strong>Accounts:</strong> you are responsible for accurate registration details, keeping login credentials confidential, securing your devices, reporting unauthorized access, and keeping your account information current. Accounts may be suspended or terminated for fraud, abuse, unauthorized access, or material breach.</li>
              <li><strong>Project requests:</strong> submitting a request does not constitute acceptance. Scope, specifications, deliverables, milestones, timeline, pricing, payment schedule, ownership, hosting, support, warranties, and termination are confirmed in writing before development begins.</li>
              <li><strong>Products:</strong> N.O.U. delivers products through websites, Progressive Web Applications (PWAs), Android, desktop, hosted software, SaaS, APIs, enterprise systems, and client-specific software, under the conditions stated on the relevant product page or agreement.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>2. Software Products, Licensing and Distribution</h2>
            <p className={sub}>
              Unless a written agreement expressly states otherwise, purchasing or accessing an N.O.U.
              software product does not transfer ownership of the underlying source code or N.O.U.&apos;s
              intellectual property.
            </p>
            <ul className={list + ' mt-3'}>
              <li><strong>Hosted software:</strong> N.O.U. may host the application, database, and infrastructure; customers receive authorized access, not backend source code or credentials.</li>
              <li><strong>Web apps &amp; PWAs:</strong> access does not grant source code, backend code, database credentials, deployment configuration, private APIs, or infrastructure.</li>
              <li><strong>Android apps:</strong> distributed through authorized marketplaces; customers receive the compiled application and the applicable right to use it, not the source code or keys.</li>
              <li><strong>Downloads:</strong> packages may contain installers, components, instructions, documentation, release notes, and licence information, protected by versioning and access controls.</li>
              <li><strong>Updates:</strong> N.O.U. may release security, bug-fix, feature, compatibility, and performance updates through the applicable channel.</li>
              <li><strong>Prohibited:</strong> reverse engineering, extracting source code, circumventing protections, unauthorized redistribution or resale, sublicensing, removing notices, interfering with security, or unlawful use.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>3. Privacy Policy</h2>
            <p className={sub}>
              N.O.U. collects, uses, stores, protects, and discloses personal data in line with its
              Privacy Policy and applicable Kenyan law, including the Data Protection Act, 2019.
              See our{' '}
              <Link to="/privacy" className="text-primary-600 hover:text-primary-700 underline">Privacy Policy</Link>{' '}
              for details on what we collect, why, how it is shared, retained, and secured, and your
              data-subject rights.
            </p>
          </div>

          <div className={section}>
            <h2 className={heading}>4. Developer Employment and Engagement</h2>
            <p className={sub}>
              Developers may work with N.O.U. as employees, fixed-term employees, independent
              contractors, consultants, or project-based developers. The applicable relationship is
              specified in the individual agreement and governed by applicable Kenyan employment law.
            </p>
            <ul className={list + ' mt-3'}>
              <li><strong>Contract duration:</strong> where a fixed-term contract is used, its duration is stated in the employment agreement. Any minimum contractual period remains subject to applicable employment law and lawful termination rights.</li>
              <li><strong>Duties:</strong> perform assigned work professionally, meet agreed requirements and standards, protect company and customer information, report progress accurately, meet reasonable deadlines, and comply with lawful instructions.</li>
              <li><strong>Compensation &amp; probation:</strong> as stated in the applicable agreement, with statutory deductions handled according to Kenyan law; probation administered per the agreement and law.</li>
              <li><strong>Termination:</strong> handled per the agreement, Kenyan employment law, and company policies, following the applicable legal process for misconduct, poor performance, incapacity, or other statutory grounds. Redundancy follows applicable requirements.</li>
              <li><strong>Exit obligations:</strong> return company property, securely delete or return company information where instructed, surrender credentials, cease unauthorized access, and honour continuing confidentiality and intellectual-property obligations.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>5. Company Policies for Developers</h2>
            <ul className={list}>
              <li><strong>Professional conduct:</strong> act honestly, respect colleagues and customers, avoid harassment, discrimination, and unfair conduct, and accurately represent work and progress.</li>
              <li><strong>System security:</strong> never share passwords, expose API keys, publish private credentials, commit secrets to public repositories, access systems without authorization, copy customer databases without authorization, or bypass security controls.</li>
              <li><strong>Confidentiality:</strong> protect non-public information about N.O.U., customers, investors, employees, source code, databases, credentials, strategies, pricing, and unreleased products. Obligations may continue after leaving.</li>
              <li><strong>External tools:</strong> use external tools and services responsibly; never submit confidential customer information, passwords, private keys, or restricted source code to external services unless authorized. Assisted work remains subject to review, testing, and approval.</li>
              <li><strong>Intellectual property:</strong> work created within the scope of engagement is governed by the company&apos;s IP provisions; disclose third-party or pre-existing IP incorporated into company projects.</li>
              <li><strong>Projects &amp; deadlines:</strong> projects are managed through approved systems; delays must be reported to the team leader or manager as soon as reasonably possible, and extensions are granted through company procedures.</li>
              <li><strong>Quality assurance:</strong> completed software may undergo code, functional, security, performance, compatibility, and acceptance testing; only approved releases are published.</li>
              <li><strong>Attendance, conflicts &amp; discipline:</strong> observe agreed working arrangements; disclose actual or potential conflicts of interest; disciplinary matters follow applicable law and policy, and employees may raise grievances without retaliation.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>6. Intellectual Property and Confidentiality</h2>
            <ul className={list}>
              <li><strong>N.O.U. IP:</strong> trademarks, logos, software, source code, databases, APIs, documentation, designs, business processes, and proprietary materials remain N.O.U.&apos;s unless otherwise agreed.</li>
              <li><strong>Customer IP:</strong> customers retain ownership of their pre-existing IP and are responsible for having the rights to provide any materials shared with N.O.U.</li>
              <li><strong>Custom project ownership:</strong> ownership of newly developed deliverables is determined by the written project agreement, which may assign, license, retain, or co-own deliverables as agreed.</li>
              <li><strong>Open source:</strong> where open-source components are used, N.O.U. complies with the applicable licence conditions, and customers may be subject to third-party open-source licences.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>7. Project Development and Client Engagement</h2>
            <ul className={list}>
              <li><strong>Lifecycle:</strong> Customer Request → Requirements Analysis → Technical Assessment → Proposal/Quotation → Customer Approval → Project Agreement → Development → Testing → Customer Review → Deployment → Maintenance/Support.</li>
              <li><strong>Scope changes:</strong> changes after scope approval may affect cost, timeline, resources, architecture, and delivery date; material changes are documented and approved before implementation.</li>
              <li><strong>Hosting:</strong> projects may be N.O.U.-hosted, client-hosted, hybrid, or standalone, as stated in the project agreement.</li>
              <li><strong>Maintenance &amp; support:</strong> development does not automatically include unlimited future maintenance; support is provided under a maintenance agreement, subscription, SLA, warranty, or separate arrangement.</li>
              <li><strong>Acceptance:</strong> where acceptance is required, the agreement specifies the procedure, including the review period for reporting material defects.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>8. General Terms and Dispute Resolution</h2>
            <ul className={list}>
              <li><strong>Amendments:</strong> N.O.U. may update these Terms; material changes will be communicated through the website, application, account notification, email, or another reasonable method, with the effective date displayed.</li>
              <li><strong>Separate agreements:</strong> these Terms do not replace employment contracts, project agreements, licences, SLAs, or confidentiality agreements, which govern to the extent of any inconsistency.</li>
              <li><strong>Severability &amp; waiver:</strong> invalid provisions are severable; failure to enforce a provision is not a permanent waiver.</li>
              <li><strong>Governing law:</strong> the laws of the Republic of Kenya, subject to mandatory legal requirements.</li>
              <li><strong>Dispute resolution:</strong> good-faith communication → negotiation → mediation or another appropriate alternative-dispute-resolution process → court proceedings where necessary. Nothing prevents approaching a competent regulator or court.</li>
              <li><strong>Regulatory rights &amp; entire agreement:</strong> these Terms, together with applicable policies and specific written agreements, constitute the applicable agreement. Acceptance may be recorded electronically with the version, date, time, and account information.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>9. Contact Information</h2>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-sm text-gray-600 space-y-1">
              <p><strong>N.O.U. Digital Systems</strong> · Website: nou.com · Country: Kenya</p>
              <p>General Contact: <a href="mailto:noudigitalsystem@gmail.com" className="text-primary-600 hover:text-primary-700">noudigitalsystem@gmail.com</a></p>
              <p>Legal Contact: 079298662</p>
              <p>Privacy Contact: <a href="mailto:nouprivacy@gmail.com" className="text-primary-600 hover:text-primary-700">nouprivacy@gmail.com</a></p>
              <p>Business/Physical Address: Kisumu</p>
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-gray-200">
            <Link to="/privacy" className="btn-secondary">Read the Privacy Policy</Link>
            <Link to="/" className="btn-outline ml-3">Back to home</Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TermsPage
